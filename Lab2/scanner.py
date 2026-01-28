import nmap

try:
    nm = nmap.PortScanner()
    active = True

    while active:
        target = input("\nEnter IP to scan (or 'exit' to quit): ")
        
        if target.lower() == 'exit':
            active = False
            continue

        print(f"--- Starting Scan on {target} ---")
        
        #we perform the scan once
        #if it fails it will hit the outer exception handle
        nm.scan(target, '20-1024', arguments='-sT') 

        hosts_list = nm.all_hosts()

        #using a simple if/else for host discovery logic
        if not hosts_list:
            print(f"No response from {target}. Check permissions or connectivity.")
        else:
            #for loop to iterate through discovered hosts
            for host in hosts_list:
                hostname = nm[host].hostname()
                state = nm[host].state()
                
                print(f"\nHost : {host} ({hostname})")
                print(f"State: {state}")

                #for loop to iterate through protocols (TCP/UDP)
                for proto in nm[host].all_protocols():
                    print(f"Protocol: {proto}")
                    
                    #get and sort the ports
                    ports = sorted(nm[host][proto].keys())
                    
                    #for loop to iterate through individual ports
                    for port in ports:
                        port_state = nm[host][proto][port]['state']
                        service_name = nm[host][proto][port]['name']
                        print(f"  Port: {port}\tState: {port_state}\tService: {service_name}")

        #asks user if they want to run another scan
        retry = input("\nScan another target? (y/n): ")
        if retry.lower() != 'y':
            active = False

except nmap.PortScannerError as e:
    print(f"\nNmap error occurred: {e}")
    print("Possible causes: invalid IP/hostname, Nmap not installed, or insufficient permissions.")

except nmap.PortScannerTimeout:
    print("\nScan timed out. The host may be unreachable or blocking scans.")

except KeyboardInterrupt:
    print("\nScan interrupted by user.")

except Exception as e:
    print(f"\nUnexpected error occurred: {e}")

finally:
    print("\nScanner closed.")

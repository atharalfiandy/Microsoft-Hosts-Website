import os
import sys
import time
import subprocess
import http.server
import socketserver
import threading
import webbrowser

# Colors for terminal output
GREEN = "\033[92m"
RESET = "\033[0m"

def check_admin():
    """Hosts file modification requires Administrator / Superuser rights."""
    try:
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False

def add_to_hosts(domain):
    """Maps custom domain to local machine inside system hosts file."""
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if os.name == 'nt' else "/etc/hosts"
    entry = f"\n127.0.0.1 {domain}\n"
    
    try:
        with open(hosts_path, "r") as f:
            content = f.read()
        if domain not in content:
            with open(hosts_path, "a") as f:
                f.write(entry)
            print(f"Added {domain} to hosts file.")
    except Exception as e:
        print(f"Failed to update hosts file: {e}")

def run_server(folder_path, port=80):
    """Starts a local server serving files from the chosen path."""
    os.chdir(folder_path)
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Server running port {port}...")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

def main():
    if not check_admin():
        print("Please run this script with Administrator / Sudo privileges to enable custom domain hosting.")
        input("Press Enter to exit...")
        sys.exit()

    # Step 1: Prompt 1
    input1 = input("when you html and files turn into hosts website: ").strip().lower()
    if input1 != "yes":
        print("Exiting...")
        return

    # Step 2: Folder path input
    path = input("Enter path html and files folder: ").strip().strip('"').strip("'")
    if not os.path.exists(path):
        print("Path does not exist. Please restart and enter a valid directory.")
        return

    # Step 3: Custom domain input validation (.com, .net, http://)
    while True:
        domain_input = input("Enter custom host (must start with http:// and end with .com or .net, e.g. http://mywebsite.com): ").strip()
        
        # Strip protocol prefix if provided
        clean_domain = domain_input
        if clean_domain.startswith("https://"):
            clean_domain = clean_domain[8:]
        elif clean_domain.startswith("http://"):
            clean_domain = clean_domain[7:]

        # Validate domain ending
        if clean_domain.endswith(".com") or clean_domain.endswith(".net"):
            break
        else:
            print("Invalid domain format! Domain must end with .com or .net")

    # Step 4: Print "virtual_hosts.wanb" 10 times in green
    for _ in range(10):
        print(f"{GREEN}virtual_hosts.wanb{RESET}")

    # Step 5: Apply custom domain setup
    add_to_hosts(clean_domain)

    # Step 6: Start background web server on Port 80 (HTTP)
    server_thread = threading.Thread(target=run_server, args=(path, 80), daemon=True)
    server_thread.start()

    time.sleep(0) # Give server time to bind

    # Step 7: Open site in default browser using custom domain name
    url_to_open = f"http://{clean_domain}"
    print(f"Opening website at: {url_to_open}")
    webbrowser.open(url_to_open)

    # Step 8: Keep Python script open so website remains active without crashing
    print("\nWebsite is live! Keep this Python window open.")
    print("Press Ctrl+C inside this window to stop hosting.")
    
    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        print("\nStopping host service...")

if __name__ == "__main__":
    main()

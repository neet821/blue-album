#!/usr/bin/env python3
"""
Environment validation script
Checks if the environment is properly configured before deployment
"""
import sys
import os
import platform
import subprocess
from pathlib import Path

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_status(status: str, message: str):
    """Print colored status message"""
    if status == "OK":
        print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
        return True
    elif status == "WARN":
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")
        return True
    elif status == "ERROR":
        print(f"{Colors.RED}✗{Colors.RESET} {message}")
        return False
    else:
        print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")
        return True

def run_command(cmd: str) -> tuple[bool, str]:
    """Run shell command and return (success, output)"""
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_python():
    """Check Python version"""
    print(f"\n{Colors.BOLD}1. Python Environment{Colors.RESET}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_status("OK", f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_status("ERROR", f"Python {version.major}.{version.minor} (requires 3.8+)")
        return False

def check_node():
    """Check Node.js version"""
    print(f"\n{Colors.BOLD}2. Node.js Environment{Colors.RESET}")
    success, output = run_command("node --version")
    if success:
        version = output.replace('v', '')
        major_version = int(version.split('.')[0])
        if major_version >= 16:
            print_status("OK", f"Node.js {version}")
            return True
        else:
            print_status("WARN", f"Node.js {version} (recommends 18+)")
            return True
    else:
        print_status("ERROR", "Node.js not found")
        return False

def check_mysql():
    """Check MySQL/MariaDB"""
    print(f"\n{Colors.BOLD}3. Database (MySQL/MariaDB){Colors.RESET}")
    
    # Try mysql command
    success, output = run_command("mysql --version")
    if success:
        print_status("OK", f"MySQL/MariaDB installed: {output.split()[0]}")
        return True
    
    # Try checking if service is running (Linux)
    if platform.system() == "Linux":
        success, _ = run_command("systemctl is-active mysql")
        if success:
            print_status("OK", "MySQL service is running")
            return True
        
        success, _ = run_command("systemctl is-active mariadb")
        if success:
            print_status("OK", "MariaDB service is running")
            return True
    
    print_status("WARN", "MySQL client not found (may be installed but not in PATH)")
    return True

def check_docker():
    """Check Docker (optional)"""
    print(f"\n{Colors.BOLD}4. Docker (Optional){Colors.RESET}")
    success, output = run_command("docker --version")
    if success:
        print_status("OK", f"Docker installed: {output}")
        
        # Check docker-compose
        success, output = run_command("docker-compose --version")
        if success:
            print_status("OK", f"Docker Compose installed: {output}")
        else:
            success, output = run_command("docker compose version")
            if success:
                print_status("OK", f"Docker Compose (v2) installed: {output}")
            else:
                print_status("WARN", "Docker Compose not found")
        return True
    else:
        print_status("INFO", "Docker not installed (optional for traditional deployment)")
        return True

def check_nginx():
    """Check Nginx (for production)"""
    print(f"\n{Colors.BOLD}5. Nginx (Production){Colors.RESET}")
    success, output = run_command("nginx -v")
    if success:
        print_status("OK", f"Nginx installed: {output}")
        
        # Check if nginx is running (Linux)
        if platform.system() == "Linux":
            success, _ = run_command("systemctl is-active nginx")
            if success:
                print_status("OK", "Nginx service is running")
            else:
                print_status("WARN", "Nginx is installed but not running")
        return True
    else:
        print_status("INFO", "Nginx not found (required for production deployment)")
        return True

def check_git():
    """Check Git"""
    print(f"\n{Colors.BOLD}6. Git{Colors.RESET}")
    success, output = run_command("git --version")
    if success:
        print_status("OK", f"Git installed: {output}")
        return True
    else:
        print_status("ERROR", "Git not found")
        return False

def check_ports():
    """Check if required ports are available"""
    print(f"\n{Colors.BOLD}7. Port Availability{Colors.RESET}")
    
    import socket
    ports_to_check = {
        3306: "MySQL",
        8000: "Backend API",
        80: "HTTP (Nginx)",
        443: "HTTPS (Nginx)"
    }
    
    all_ok = True
    for port, service in ports_to_check.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))
                if result == 0:
                    print_status("WARN", f"Port {port} ({service}) is in use")
                else:
                    print_status("OK", f"Port {port} ({service}) is available")
        except Exception as e:
            print_status("WARN", f"Could not check port {port}: {e}")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Check if .env file exists"""
    print(f"\n{Colors.BOLD}8. Environment Configuration{Colors.RESET}")
    
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if env_file.exists():
        print_status("OK", ".env file exists")
        
        # Check required variables
        with open(env_file) as f:
            content = f.read()
            required_vars = [
                "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME",
                "SECRET_KEY"
            ]
            missing = [var for var in required_vars if var not in content]
            
            if missing:
                print_status("WARN", f"Missing variables: {', '.join(missing)}")
            else:
                print_status("OK", "All required variables present")
        
        return True
    elif env_example.exists():
        print_status("WARN", ".env file not found (copy from .env.example)")
        return False
    else:
        print_status("ERROR", "Neither .env nor .env.example found")
        return False

def check_python_packages():
    """Check if Python packages are installed"""
    print(f"\n{Colors.BOLD}9. Python Dependencies{Colors.RESET}")
    
    project_root = Path(__file__).parent.parent
    requirements = project_root / "backend" / "requirements.txt"
    
    if not requirements.exists():
        print_status("WARN", "requirements.txt not found")
        return False
    
    try:
        import fastapi
        import sqlalchemy
        import pymysql
        print_status("OK", "Core Python packages installed")
        return True
    except ImportError as e:
        print_status("ERROR", f"Missing Python packages: {e.name}")
        print_status("INFO", "Run: pip install -r backend/requirements.txt")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    print(f"\n{Colors.BOLD}10. Project Structure{Colors.RESET}")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        "backend",
        "frontend",
        "docs",
        "scripts"
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print_status("OK", f"{dir_name}/ directory exists")
        else:
            print_status("ERROR", f"{dir_name}/ directory missing")
            all_ok = False
    
    return all_ok

def main():
    """Run all checks"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 Blue Local Environment Validation{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}System Information:{Colors.RESET}")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Python: {sys.version.split()[0]}")
    
    # Run all checks
    checks = [
        check_python,
        check_node,
        check_mysql,
        check_docker,
        check_nginx,
        check_git,
        check_ports,
        check_env_file,
        check_python_packages,
        check_project_structure
    ]
    
    results = [check() for check in checks]
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Summary:{Colors.RESET}")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{Colors.GREEN}✓ All checks passed ({passed}/{total}){Colors.RESET}")
        print(f"\n{Colors.GREEN}🚀 Environment is ready for deployment!{Colors.RESET}")
        return 0
    else:
        failed = total - passed
        print(f"{Colors.YELLOW}⚠ {passed}/{total} checks passed, {failed} failed{Colors.RESET}")
        print(f"\n{Colors.YELLOW}⚠️  Please fix the issues above before deployment{Colors.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

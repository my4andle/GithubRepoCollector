# GithubRepoCollector
Sometimes you just want to use bash to grep through public source code and count how many times developers pushed passwords :)

# Usage
Usage:  
  GithubRepoCollector.py --help  
  GithubRepoCollector.py (--github_user=<github_user>)  

Options:  
  --github_user=<github_user>    Github user to scrub for projects ex: my4andle  

# Example Results
$ python3 vmware_github_scrub.py --github_user my4andle  
  
https://github.com/my4andle/vmxnet3Hunter.git  
https://github.com/my4andle/vmxnet3_hunter.git  
https://github.com/my4andle/ssh_brute.git    
https://github.com/my4andle/login_brute_forcer.git  
https://github.com/my4andle/SuperMicroHunter.git  
https://github.com/my4andle/unsecured_jenkins_discovery.git  
https://github.com/my4andle/tcpConnect.git    
https://github.com/my4andle/pymetasploit.git  
https://github.com/my4andle/apache-james-adduser.git  
https://github.com/my4andle/smtp_brute.git  
https://github.com/my4andle/port_hosts.git  
https://github.com/my4andle/massbrowser.git  
https://github.com/my4andle/wannacry_defenders_toolkit.git  
https://github.com/my4andle/oveflow_toolkit.git  

# Example clone all from results file
for a in $(cat <results_file>); do git clone $a; done

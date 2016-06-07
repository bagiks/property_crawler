# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"


  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 27017, host: 27018

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "../property_crawler", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
      	vb.memory = "2048"
  end
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL
	
	config.berkshelf.enabled = true
	config.berkshelf.berksfile_path = "./cookbooks/dev/Berksfile"		
	config.vm.provision :chef_solo do |chef|
		chef.run_list = [
			'recipe[apt]',
			'recipe[mongodb]',
			'recipe[poise-python]',
			'recipe[vim]'
		]
	end
	config.vm.provision "shell", inline: <<-SHELL
		sudo apt-get update -y
		sudo apt-get install curl -y	
	SHELL


	# config.vm.provision "shell", inline: <<-SHELL
	# 	anaconda=Anaconda2-4.0.0-Linux-x86_64.sh
	# 	cd /vagrant_data
	# 	echo -e "\n\nDownloading Anaconda installer. Take a while ..."
	# 	wget -q -O /dev/null - http://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh
	# 	if [ -s $anaconda]
	# 	then
	# 		chmod +x $anaconda
	# 		bash $anaconda

	# 	else
	# 		echo "Error: Anaconda installer is not found"
	# 	fi
	
	# SHELL
end

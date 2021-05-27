Vagrant.configure("2") do |config|

    config.vm.box = "ubuntu/focal64"

    config.vm.network "private_network", ip: "90.190.180.121", nictype: "virtio"
    config.vm.network "public_network", nictype: "virtio"

    config.vm.synced_folder ".", "/var/www/server-monitor"
    config.vm.hostname = "monitoring.dev"
    config.vm.provision "shell", path: "provision.sh"

end

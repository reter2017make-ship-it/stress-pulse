terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = "ru-central1-a"
}

resource "yandex_vpc_network" "network" {
  name = "stress-pulse-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "stress-pulse-subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "yandex_storage_bucket" "mlflow" {
  bucket     = "stress-pulse-mlflow-${random_string.suffix.result}"
  acl        = "private"
  folder_id  = var.yc_folder_id
}

resource "yandex_compute_instance" "mlflow" {
  name        = "mlflow-server"
  platform_id = "standard-v3"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = "fd80qm01ah03dkqb14lc"
      size     = 30
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_compute_instance" "airflow" {
  name        = "airflow-server"
  platform_id = "standard-v3"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = "fd80qm01ah03dkqb14lc"
      size     = 30
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

output "mlflow_ip" {
  value = yandex_compute_instance.mlflow.network_interface.0.nat_ip_address
}

output "airflow_ip" {
  value = yandex_compute_instance.airflow.network_interface.0.nat_ip_address
}

output "storage_bucket" {
  value = yandex_storage_bucket.mlflow.bucket
}

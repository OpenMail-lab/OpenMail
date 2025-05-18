provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "openmail" {
  metadata {
    name = "openmail"
  }
}

resource "kubernetes_deployment" "openmail" {
  metadata {
    name = "openmail"
    namespace = kubernetes_namespace.openmail.metadata[0].name
  }
}

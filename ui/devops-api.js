async function fetchDevOpsStatus() {
  const tools = ["kiali", "terraform", "argocd", "helm", "ansible", "docker"];
  for (let tool of tools) {
    let response = await fetch(`/api/status/${tool}`);
    let status = await response.json();
    document.getElementById(`${tool}-status`).innerText = status.running ? "✅ Running" : "❌ Stopped";
  }
}

setInterval(fetchDevOpsStatus, 5000);

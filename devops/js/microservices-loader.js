const SERVICES = {
    kiali: { port: 31001, icon: '🌐' },
    terraform: { port: 31002, icon: '⚙️' },
    argocd: { port: 31003, icon: '🔄' },
    helm: { port: 31004, icon: '📦' },
    ansible: { port: 31005, icon: '🔁' },
    docker: { port: 31006, icon: '🐳' },
    kubernetes: { port: 31007, icon: '☸️' },
    jenkins: { port: 31008, icon: '🔧' },
    trivy: { port: 31009, icon: '🔍' },
    prometheus: { port: 31010, icon: '📊' }
};

function loadService(service) {
    fetch(`http://localhost:${service.port}/status`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('terminal').innerHTML += 
                `\n> Loading ${service.name}...`;
        })
        .catch(err => console.error(`Error loading ${service.name}:`, err));
}

function openTerminal(tool) {
    const terminal = document.getElementById('terminal');
    switch(tool) {
        case 'istio':
            terminal.innerHTML += '\n> istioctl version';
            fetch('http://localhost:31011/istio/status')
                .then(response => response.text())
                .then(data => {
                    terminal.innerHTML += '\n' + data;
                });
            break;
        case 'minikube':
            terminal.innerHTML += '\n> minikube status';
            fetch('http://localhost:31013/minikube/status')
                .then(response => response.text())
                .then(data => {
                    terminal.innerHTML += '\n' + data;
                });
            break;
    }
    terminal.scrollTop = terminal.scrollHeight;
}

class TerminalHandler {
    constructor() {
        this.terminal = document.getElementById('terminal');
        this.commandHistory = [];
        this.historyIndex = -1;
    }

    async handleIstioCommand(command) {
        this.terminal.innerHTML += `\n$ ${command}`;
        
        if (command.startsWith('istioctl')) {
            const response = await fetch('/packages/istio/api/execute', {
                method: 'POST',
                body: JSON.stringify({ command })
            });
            
            const result = await response.text();
            this.terminal.innerHTML += `\n${result}`;
        }

        this.terminal.scrollTop = this.terminal.scrollHeight;
    }

    clear() {
        this.terminal.innerHTML = '> Terminal Ready';
    }
}

const terminal = new TerminalHandler();

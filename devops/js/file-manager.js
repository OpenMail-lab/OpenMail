class FileManager {
    static async init(configPath) {
        const config = await this.loadConfig(configPath);
        await this.loadStyles(config.filePaths.styles);
        await this.loadScripts(config.filePaths.scripts);
        await this.loadComponents(config.filePaths.components);
    }

    static async loadConfig(path) {
        const response = await fetch(path);
        const config = await response.json();
        window.appConfig = config;
        return config;
    }

    static async loadStyles(paths) {
        paths.forEach(path => {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = `devops/${path}`;
            document.head.appendChild(link);
        });
    }

    static async loadScripts(paths) {
        for (const path of paths) {
            await import(`/devops/${path}`);
        }
    }

    static async loadComponents(paths) {
        const root = document.getElementById('root');
        for (const path of paths) {
            const response = await fetch(`devops/${path}`);
            const html = await response.text();
            const div = document.createElement('div');
            div.innerHTML = html;
            root.appendChild(div);
        }
    }
}

class PackageLoader {
    constructor() {
        this.loadedPackages = new Set();
        this.terminal = document.getElementById('terminal');
    }

    async loadPackage(name) {
        if (this.loadedPackages.has(name)) return true;
        
        try {
            this.terminal.innerHTML += `\n> Loading ${name} package...`;
            const response = await fetch(`${LOCAL_PACKAGES[name]}/manifest.json`);
            const manifest = await response.json();
            
            // Load package dependencies
            for (const dep of manifest.dependencies || []) {
                await this.loadPackage(dep);
            }
            
            this.loadedPackages.add(name);
            this.terminal.innerHTML += `\n> ${name} package loaded successfully`;
            return true;
        } catch (err) {
            this.terminal.innerHTML += `\n> Error loading ${name}: ${err.message}`;
            return false;
        }
    }
}

const packageLoader = new PackageLoader();

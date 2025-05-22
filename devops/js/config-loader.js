class ConfigLoader {
    async loadConfig() {
        const response = await fetch('/packages/config.json');
        const config = await response.json();
        window.appConfig = config;
        
        // Initialize theme
        const themeManager = new ThemeManager(config.theme);
        themeManager.applyTheme();
        
        // Initialize effects
        if (config.theme.effects.particles) {
            initParticles();
        }
        if (config.theme.effects.hologram) {
            initHologram();
        }
        
        return config;
    }
}

const configLoader = new ConfigLoader();
document.addEventListener('DOMContentLoaded', () => configLoader.loadConfig());

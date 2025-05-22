class ThemeManager {
    constructor(themeConfig) {
        this.config = themeConfig;
    }

    applyTheme() {
        document.documentElement.style.setProperty('--neon-primary', this.config.primary);
        document.documentElement.style.setProperty('--neon-secondary', this.config.secondary);
        document.documentElement.style.setProperty('--cyber-bg', this.config.background);

        if (this.config.effects.neonText) {
            document.querySelectorAll('.tools-menu button').forEach(btn => {
                btn.classList.add('neon-text');
            });
        }
    }
}

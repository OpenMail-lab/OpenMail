class HoloEffect {
    constructor() {
        this.canvas = document.getElementById('holoLogo');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
    }

    createParticles() {
        for(let i = 0; i < 100; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                speed: Math.random() * 2 + 1,
                radius: Math.random() * 2
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.particles.forEach(p => {
            p.y -= p.speed;
            if(p.y < 0) p.y = this.canvas.height;
            
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = '#00f3ff';
            this.ctx.fill();
        });
        requestAnimationFrame(() => this.animate());
    }
}

const holo = new HoloEffect();
holo.createParticles();
holo.animate();

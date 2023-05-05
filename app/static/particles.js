const NUM_PARTICLES = 50;
const PARTICLE_SIZE = 10;

const particles = [];

document.addEventListener('mousedown', (event) => {
  for (let i = 0; i < particles.length; i++) {
    const particle = particles[i];
    const rect = particle.getBoundingClientRect();
    const centerX = rect.left + PARTICLE_SIZE / 2;
    const centerY = rect.top + PARTICLE_SIZE / 2;
    const dx = event.clientX - centerX;
    const dy = event.clientY - centerY;
    const distance = Math.sqrt(dx * dx + dy * dy);
    particle.vx = (dx / distance) * 10;
    particle.vy = (dy / distance) * 10;
  }
});

document.addEventListener('mouseup', () => {
  for (let i = 0; i < particles.length; i++) {
    const particle = particles[i];
    particle.vx = (Math.random() - 0.5) * 5;
    particle.vy = (Math.random() - 0.5) * 5;
  }
});


function createParticle() {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.top = `${Math.random() * window.innerHeight}px`;
    particle.style.left = `${Math.random() * window.innerWidth}px`;

    // Generate a random pastel color for each particle
    const hue = Math.floor(Math.random() * 360);
    const pastel = `hsl(${hue}, 50%, 80%)`;
    particle.style.backgroundColor = pastel;

    document.body.appendChild(particle);
    particles.push(particle);
  }
  

  function updateParticles() {
    for (let i = 0; i < particles.length; i++) {
      const particle = particles[i];
      let x = parseInt(particle.style.left);
      let y = parseInt(particle.style.top);
      let vx = particle.vx || (Math.random() - 0.5) * 5;
      let vy = particle.vy || (Math.random() - 0.5) * 5;
      x += vx;
      y += vy;
      if (x < 0 || x > window.innerWidth - PARTICLE_SIZE) {
        vx *= -1;
      }
      if (y < 0 || y > window.innerHeight - PARTICLE_SIZE) {
        vy *= -1;
      }
      particle.style.left = `${x}px`;
      particle.style.top = `${y}px`;
      particle.vx = vx;
      particle.vy = vy;
    }
  }
  

for (let i = 0; i < NUM_PARTICLES; i++) {
  createParticle();
}

setInterval(updateParticles, 20);

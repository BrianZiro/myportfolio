// ================================
// Portfolio Interactivity & Animations
// ================================

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href"))
      .scrollIntoView({ behavior: "smooth" });
  });
});

// Mobile menu toggle
const mobileBtn = document.getElementById("mobile-menu-button");
const mobileMenu = document.getElementById("mobile-menu");

if (mobileBtn) {
  mobileBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("hidden");
    mobileBtn.classList.toggle("open");
  });
}

// Scroll reveal effect
const sections = document.querySelectorAll("section");
const revealOnScroll = () => {
  const triggerBottom = window.innerHeight * 0.85;
  sections.forEach(sec => {
    const top = sec.getBoundingClientRect().top;
    if (top < triggerBottom) {
      sec.classList.add("visible");
    }
  });
};
window.addEventListener("scroll", revealOnScroll);
revealOnScroll();

// Typing effect for tagline
function typeEffect(element, text, speed = 100) {
  let i = 0;
  function typing() {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(typing, speed);
    }
  }
  typing();
}
const tagline = document.querySelector(".tagline");
if (tagline) {
  typeEffect(tagline, "Actuarial Science • Data Science • Machine Learning • Django", 80);
}

// Theme toggle
const themeToggle = document.getElementById("theme-toggle");
if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  });
}

// Load theme from storage
const storedTheme = localStorage.getItem("theme");
if (storedTheme) {
  document.documentElement.setAttribute("data-theme", storedTheme);
}

// Background particles
const particleContainer = document.createElement("div");
particleContainer.classList.add("particles");
document.body.appendChild(particleContainer);

for (let i = 0; i < 20; i++) {
  const particle = document.createElement("div");
  particle.classList.add("particle");
  particle.style.width = particle.style.height = `${Math.random() * 8 + 4}px`;
  particle.style.left = `${Math.random() * 100}%`;
  particle.style.top = `${Math.random() * 100}%`;
  particle.style.animationDuration = `${Math.random() * 8 + 5}s`;
  particleContainer.appendChild(particle);
}

// ================================
// Project Card Popup
// ================================
const cards = document.querySelectorAll(".card");
const modal = document.createElement("div");
modal.classList.add("modal");
modal.innerHTML = `
  <div class="modal-content">
    <span class="modal-close">&times;</span>
    <div class="modal-body"></div>
  </div>
`;
document.body.appendChild(modal);

const modalContent = modal.querySelector(".modal-body");
const closeBtn = modal.querySelector(".modal-close");

// Open modal on card click
cards.forEach(card => {
  card.addEventListener("click", () => {
    const clone = card.cloneNode(true);
    modalContent.innerHTML = "";
    modalContent.appendChild(clone);
    modal.classList.add("active");
  });
});

// Close modal
closeBtn.addEventListener("click", () => {
  modal.classList.remove("active");
});

// Close when clicking outside content
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.remove("active");
  }
});

//CHATBOT
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("chatbot-toggle");
    const container = document.getElementById("chatbot-container");
    const closeBtn = document.getElementById("chatbot-close");
    const input = document.getElementById("chatbot-input");
    const sendBtn = document.getElementById("chatbot-send");
    const messages = document.getElementById("chatbot-messages");

    // Show default greeting once
    function addGreeting() {
        if (messages.children.length === 0) {
            const botBubble = document.createElement("div");
            botBubble.className = "bot";
            botBubble.textContent = "Hello 👋! Ask me anything.";
            messages.appendChild(botBubble);
        }
    }

    // Toggle chatbot
    toggle.addEventListener("click", () => {
        container.style.display = (container.style.display === "none" || !container.style.display) ? "flex" : "none";
        addGreeting();
    });

    closeBtn.addEventListener("click", () => container.style.display = "none");

    async function sendMessage() {
        const userMsg = input.value.trim();
        if (!userMsg) return;

        // Remove greeting if it's still there
        if (messages.children.length === 1 && messages.children[0].textContent.includes("Hello")) {
            messages.innerHTML = "";
        }

        // User bubble
        const userBubble = document.createElement("div");
        userBubble.className = "user";
        userBubble.textContent = userMsg;
        messages.appendChild(userBubble);

        input.value = "";
        messages.scrollTop = messages.scrollHeight;

        // Send to backend
        try {
            const response = await fetch("/chatbot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ message: userMsg })
            });

            const data = await response.json();

            const botBubble = document.createElement("div");
            botBubble.className = "bot";
            botBubble.textContent = data.reply || "⚠️ No response received";
            messages.appendChild(botBubble);
            messages.scrollTop = messages.scrollHeight;

        } catch (err) {
            console.error(err);
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", e => { if (e.key === "Enter") sendMessage(); });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";").map(c => c.trim());
        for (let cookie of cookies) {
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

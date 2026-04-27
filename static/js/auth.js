(function () {
  const toggles = document.querySelectorAll("[data-password-toggle]");

  toggles.forEach(function (button) {
    button.addEventListener("click", function () {
      const inputWrap = button.closest(".input-wrap");
      if (!inputWrap) return;

      const input = inputWrap.querySelector("[data-password-input]");
      if (!input) return;

      const showPassword = input.type === "password";
      input.type = showPassword ? "text" : "password";
      button.setAttribute("aria-label", showPassword ? "Ocultar contrasena" : "Mostrar contrasena");

      const icon = button.querySelector("[data-password-icon]");
      if (icon) {
        icon.setAttribute("data-lucide", showPassword ? "eye-off" : "eye");
        if (window.lucide && typeof window.lucide.createIcons === "function") {
          window.lucide.createIcons();
        }
      }
    });
  });
})();

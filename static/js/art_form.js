
  document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[type="file"]');
    const preview = document.getElementById('imagePreview');

    input.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          preview.src = e.target.result;
          preview.classList.remove('hidden');
        }
        reader.readAsDataURL(file);
      }
    });
  });

document.addEventListener("DOMContentLoaded", function() {

  function openModal(modal) {
    modal.style.display = "block";

    // Close button sa sulod ka modal
    const closeBtn = modal.querySelector(".close, .close-btn");
    if (closeBtn) {
      closeBtn.onclick = () => modal.style.display = "none";
    }

    // ma close kung pindot outside ka modal
    window.onclick = function(e) {
      if (e.target == modal) {
        modal.style.display = "none";
      }
    }
  }

  // Ma Open Add Subject modal
  const addModal = document.getElementById("subjectModal");
  const openAddBtn = document.getElementById("openModalSubject");
  openAddBtn.onclick = function(e) {
    e.preventDefault();
    openModal(addModal);
  }

  //  Ma Open Edit/Delete modals
  document.querySelectorAll(".edit-btn, .delete-btn").forEach(btn => {
    btn.addEventListener("click", function(e) {
      e.preventDefault();
      const modalId = btn.dataset.target;
      const modal = document.querySelector(modalId);
      openModal(modal);
    });
  });
});

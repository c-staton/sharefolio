function animateOnScroll(eleId, animateClass) {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add(animateClass);
        }
        });
    });

    observer.observe(document.getElementById(eleId));
    return
}
  
animateOnScroll('main-img', 'slide-left');

animateOnScroll('main-info', 'fade-in');
animateOnScroll('first-info', 'fade-in');
animateOnScroll('second-info', 'fade-in');
animateOnScroll('third-info', 'fade-in');

  
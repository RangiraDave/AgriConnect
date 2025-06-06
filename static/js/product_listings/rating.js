// Rating System
function initRatingSystem() {
    document.querySelectorAll('.rating-form').forEach(form => {
        const stars = form.querySelectorAll('.star');
        const ratingInput = form.querySelector('.rating-value');
        const submitButton = form.querySelector('.submit-rating');

        stars.forEach(star => {
            star.addEventListener('click', function() {
                const rating = this.getAttribute('data-value');
                ratingInput.value = rating;
                highlightStars(stars, rating);
                submitButton.style.display = 'block';
            });

            star.addEventListener('mouseover', function() {
                const rating = this.getAttribute('data-value');
                highlightStars(stars, rating);
            });
        });

        form.addEventListener('mouseleave', function() {
            const currentRating = ratingInput.value;
            highlightStars(stars, currentRating);
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    showToast('Rating submitted successfully!');
                    submitButton.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error submitting rating');
            });
        });
    });
}

function highlightStars(stars, rating) {
    stars.forEach(star => {
        const value = star.getAttribute('data-value');
        if (value <= rating) {
            star.classList.add('text-warning');
        } else {
            star.classList.remove('text-warning');
        }
    });
}

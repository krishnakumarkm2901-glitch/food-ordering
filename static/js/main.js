const addToCartButtons = document.querySelectorAll('.add-to-cart');
const cartCountElement = document.getElementById('cart-count');

if (addToCartButtons) {
    addToCartButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const itemId = button.dataset.itemId;
            const response = await fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ item_id: itemId })
            });

            const result = await response.json();
            if (result.success && cartCountElement) {
                cartCountElement.textContent = result.cart_count;
                button.textContent = 'Added';
                button.disabled = true;
                setTimeout(() => {
                    button.textContent = 'Add to cart';
                    button.disabled = false;
                }, 1200);
            }
        });
    });
}

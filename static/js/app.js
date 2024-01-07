document.addEventListener('DOMContentLoaded', function () {

    // Add event listeners to all 'Add to Cart' buttons
    document.querySelectorAll('.add-to-cart-button').forEach(button => {
        button.onclick = () => {
            const productId = button.dataset.productId;
            addToCart(productId);
        };
    });

    // Add event listeners to all 'Remove from Cart' buttons
    document.querySelectorAll('.remove-from-cart-button').forEach(button => {
        button.onclick = () => {
            const productId = button.dataset.productId;
            removeFromCart(productId);
        };
    });

    // Function to add a product to the cart
    function addToCart(productId) {
        fetch(`/add_to_cart/${productId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartDisplay(data.cart);
                } else {
                    console.error('Error adding item to cart:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Function to remove a product from the cart
    function removeFromCart(productId) {
        fetch(`/remove_from_cart/${productId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartDisplay(data.cart);
                } else {
                    console.error('Error removing item from cart:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Function to update the cart display
    function updateCartDisplay(cart) {
        const cartContainer = document.getElementById('cart-container');
        // Clear current cart contents
        cartContainer.innerHTML = '';
        // Add new cart items to the display
        cart.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.innerHTML = `${item.name} - Quantity: ${item.quantity}`;
            cartContainer.appendChild(itemElement);
        });
    }

});

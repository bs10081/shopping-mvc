mounted() {
    this.getCart();
  },
  methods: {
    async getCart() {
      try {
        const response = await axios.get('/api/customer?act=showCartList');
        this.cartItems = response.data;
      } catch (error) {
        console.error('無法獲取購物車內容:', error);
      }
    }
  }
  
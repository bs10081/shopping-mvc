
<template>
    <div>
        <template>
            <div>
                <h2>商品列表</h2>
                <ul>
                    <li v-for="product in products" :key="product.pID">
                        <h3>{{ product.name }}</h3>
                        <p>價格: {{ product.price }}</p>
                        <p>描述: {{ product.content }}</p>
                        <!-- 其他商品資訊 -->
                    </li>
                </ul>
            </div>
        </template>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            products: []
        };
    },
    mounted() {
        this.getProducts();
    },

    methods: {
        async getProducts() {
            try {
                const response = await axios.get('/api/customer?act=showProductList');
                this.products = response.data;
            } catch (error) {
                console.error('無法獲取商品列表:', error);
            }
        },
        async addToCart(productId) {
            try {
                await axios.get(`/api/customer?act=addCart&id=${productId}`);
                alert('商品已加入購物車');
            } catch (error) {
                console.error('加入購物車失敗:', error);
            }
        }
    }
};
</script>

<style scoped>
ul {
    list-style-type: none;
    padding: 0;
}

li {
    border: 1px solid #ddd;
    margin: 10px 0;
    padding: 10px;
}

h3 {
    margin: 0 0 10px 0;
}

p {
    margin: 5px 0;
}
</style>

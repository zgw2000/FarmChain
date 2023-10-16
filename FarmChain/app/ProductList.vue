<template>
  <div>
    <h1>FarmChain - Products</h1>
    <ul>
      <li v-for="product in products" :key="product.id">
        {{ product.name }} - Price: {{ product.price }} - Farmer: {{ product.farmer }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    // Fetch product data from the backend API
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch('/api/products'); // Replace with your actual API endpoint
        if (response.ok) {
          this.products = await response.json();
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
  },
};
</script>

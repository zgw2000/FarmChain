<template>
  <div>
    <h2>{{ product.name }}</h2>
    <p>Price: {{ product.price }}</p>
    <p>Farmer: {{ product.farmer }}</p>
    <!-- Add more product details as needed -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      product: {},
    };
  },
  created() {
    // Fetch the product details based on the route parameter (product ID)
    const productId = this.$route.params.id;
    this.fetchProductDetails(productId);
  },
  methods: {
    async fetchProductDetails(productId) {
      try {
        const response = await axios.get(`/api/products/${productId}`); // Replace with your actual API endpoint
        this.product = response.data;
      } catch (error) {
        console.error('Error fetching product details:', error);
      }
    },
  },
};
</script>

<template>
  <form @submit.prevent="createProduct">
    <label for="productName">Product Name:</label>
    <input type="text" id="productName" v-model="newProduct.name" required>
    
    <label for="productPrice">Product Price:</label>
    <input type="number" id="productPrice" v-model="newProduct.price" required>

    <!-- Add more fields as needed -->

    <button type="submit">Create Product</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      newProduct: {
        name: '',
        price: 0,
        // Add more fields as needed
      },
    };
  },
  methods: {
    async createProduct() {
      try {
        // Send a POST request to create a new product
        await axios.post('/api/products', this.newProduct); // Replace with your actual API endpoint
        // Optionally, update the product list or perform other actions
      } catch (error) {
        console.error('Error creating product:', error);
      }
    },
  },
};
</script>

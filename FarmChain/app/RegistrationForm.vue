<!-- RegistrationForm.vue -->
<template>
  <form @submit.prevent="registerUser">
    <!-- Registration form fields (e.g., username, password) -->
    <button type="submit">Register</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      newUser: {
        username: '',
        password: '',
        // Add more fields as needed
      },
    };
  },
  methods: {
    async registerUser() {
      try {
        // Send a POST request to register a new user
        await axios.post('/api/register', this.newUser); // Replace with your actual API endpoint
        // Optionally, redirect to the login page or perform other actions
      } catch (error) {
        console.error('Error registering user:', error);
      }
    },
  },
};
</script>

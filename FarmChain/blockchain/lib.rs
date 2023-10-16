#![cfg_attr(not(feature = "std"), no_std)]

use ink_lang as ink;

#[ink::contract]
mod farmchain {
    use ink_prelude::vec::Vec;
    use ink_storage::collections::HashMap as StorageHashMap;
    use ink_storage::traits::PackedLayout;

    #[derive(Debug, PartialEq, Eq, scale::Encode, scale::Decode, PackedLayout)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub struct Product {
        name: Vec<u8>,
        price: u64,
        farmer: AccountId,
    }

    #[ink(storage)]
    pub struct FarmChain {
        products: StorageHashMap<u64, Product>,
        product_id_counter: u64,
    }

    impl FarmChain {
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                products: Default::default(),
                product_id_counter: 1,
            }
        }

        #[ink(message)]
        pub fn create_product(&mut self, name: Vec<u8>, price: u64) {
            let caller = self.env().caller();
            let product_id = self.product_id_counter;
            self.product_id_counter += 1;
            let product = Product {
                name,
                price,
                farmer: caller,
            };
            self.products.insert(product_id, product);
        }

        #[ink(message)]
        pub fn get_product(&self, product_id: u64) -> Option<Product> {
            self.products.get(&product_id).cloned()
        }

        #[ink(message)]
        pub fn list_products(&self) -> Vec<Product> {
            self.products.values().cloned().collect()
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[ink::test]
        fn create_and_get_product() {
            let mut farm_chain = FarmChain::new();
            let product_name = b"Apples".to_vec();
            let product_price = 250;
            farm_chain.create_product(product_name.clone(), product_price);
            let product = farm_chain.get_product(1).expect("Product not found");
            assert_eq!(product.name, product_name);
            assert_eq!(product.price, product_price);
        }

        #[ink::test]
        fn list_products() {
            let mut farm_chain = FarmChain::new();
            farm_chain.create_product(b"Apples".to_vec(), 250);
            farm_chain.create_product(b"Oranges".to_vec(), 180);
            let products = farm_chain.list_products();
            assert_eq!(products.len(), 2);
        }
    }
}

import FlatSiteBuilder 2.0
import ShopifyEditor 1.0

Content {
    title: "Index"
    menu: "default"
    script: "// https://shopify.github.io/js-buy-sdk/#installation

const client = window.ShopifyBuy.buildClient({
  domain: 'crowdwaredev.myshopify.com',
  storefrontAccessToken: '01fd412bcadac7389f7af39e30e56091'
});

client.product.fetchAll().then((products) => {
	var i;
	for (i=0; i < products.length; i++) {
  		alert(products[i].title);
		console.log(products[i]);
	}
});



"
    layout: "default"
    date: "2020-01-24"

    Section {

        Row {

            Column {
                span: 12

                Shopify {
                    text: "test"
                    adminlabel: "admin"
                }
            }
        }
    }
}

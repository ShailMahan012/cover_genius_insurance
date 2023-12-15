const payment_form = document.getElementById("payment-form")
const pay_btn = document.getElementById("custom_pay")

function txs_compeleted() {
  payment_form.innerHTML = `<h1 style="text-align: center;font-size: 2em;width: 100%;">
  Transaction completed, thanks for your order.
  </h1>`;
}

if (payed == true) {
  txs_compeleted()
}
else {
  pay_btn.style.display = "block"
}
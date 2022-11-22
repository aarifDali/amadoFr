$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();

        var firstname = $("[name= 'firstname']").val();
        var lastname = $("[name= 'lastname']").val();
        var email = $("[name= 'email']").val();
        var phone_number = $("[name= 'phone_number']").val();
        var address_line_1 = $("[name= 'address_line_1']").val();
        var address_line_2 = $("[name= 'address_line_2']").val();
        var city = $("[name= 'city']").val();
        var state = $("[name= 'state']").val();
        var zipcode = $("[name= 'zipcode']").val();

        if (firstname == "" || lastname == "" || email == "" || phone_number == "" || address_line_1 == "" || address_line_2 == "" || city == "" || state == "" || zipcode == "")
        {
            swal("Alert!", "All fields are mandatory", "error");
            return false;
        }
        else
        {
            $.ajax({
                type: "GET",
                url:"/place_order",
                success: function (response) {
                    var options = {
                        "key": "rzp_test_uBPf8rCnhuHijR", // Enter the Key ID generated from the Dashboard
                        "amount": "{{ payment.amount }}", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Agape Furniture",
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        "order_id": "{{ payment.id }}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (response){
                            alert(response.razorpay_payment_id);
                            
                        },
                        "prefill": {
                            "name": firstname+" "+lastname,
                            "email": email,
                            "contact": phone_number
                        },
                        
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    
                    rzp1.open();
                }
            });
            var options = {
                "key": "YOUR_KEY_ID", // Enter the Key ID generated from the Dashboard
                "amount": "50000", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Acme Corp",
                "description": "Test Transaction",
                "image": "https://example.com/your_logo",
                "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){
                    alert(response.razorpay_payment_id);
                    alert(response.razorpay_order_id);
                    alert(response.razorpay_signature)
                },
                "prefill": {
                    "name": "Gaurav Kumar",
                    "email": "gaurav.kumar@example.com",
                    "contact": "9999999999"
                },
                "notes": {
                    "address": "Razorpay Corporate Office"
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);
            
            rzp1.open();
        }

        
        
    });
});
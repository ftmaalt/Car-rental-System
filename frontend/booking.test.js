// booking.test.js
describe('Booking Form', () => {
    
    it('should submit the booking form successfully', () => {
        // Mock form data
        const bookingData = {
            carId: 1,
            startDate: '2025-11-15',
            endDate: '2025-11-20',
            customerName: 'John Doe',
            customerEmail: 'john.doe@example.com'
        };

        // Simulate form submission
        cy.visit('/booking.html'); // Adjust the path if necessary
        cy.get('input[name="carId"]').type(bookingData.carId);
        cy.get('input[name="startDate"]').type(bookingData.startDate);
        cy.get('input[name="endDate"]').type(bookingData.endDate);
        cy.get('input[name="customerName"]').type(bookingData.customerName);
        cy.get('input[name="customerEmail"]').type(bookingData.customerEmail);
        cy.get('form').submit();

        // Assert successful submission
        cy.url().should('include', '/success'); // Adjust based on your app's routing
        cy.contains('Thank you for your booking!'); // Adjust the message accordingly
    });

    it('should show validation errors for empty required fields', () => {
        cy.visit('/booking.html'); // Adjust the path if necessary
        
        // Submit the form without filling out required fields
        cy.get('form').submit();

        // Assert validation messages are displayed
        cy.contains('This field is required').should('be.visible'); // Adjust based on your validation messages
    });
});

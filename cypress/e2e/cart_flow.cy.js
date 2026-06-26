describe('Flujo del carrito de compras', () => {
  beforeEach(() => {
    cy.visit('/carrito')
  })

  it('Carga productos y muestra carrito vacío', () => {
    cy.get('#productos-container .producto-card').should('have.length.at.least', 1)
    cy.get('#carrito-container').contains('El carrito está vacío')
    cy.get('#btn-checkout').should('be.disabled')
    cy.get('#total-price').should('contain.text', '$0')
  })

  it('Agrega un producto al carrito y luego lo elimina', () => {
    cy.get('#productos-container .producto-card').first().within(() => {
      cy.get('.cantidad-input').clear().type('2')
      cy.get('.btn-agregar').click()
    })

    cy.get('#carrito-container .carrito-item').should('have.length.at.least', 1)
    cy.get('#btn-checkout').should('not.be.disabled')
    cy.get('#total-price').should('not.contain.text', '$0')

    cy.on('window:confirm', () => true)
    cy.get('#carrito-container .btn-eliminar').click()

    cy.get('#carrito-container').contains('El carrito está vacío')
    cy.get('#btn-checkout').should('be.disabled')
    cy.get('#total-price').should('contain.text', '$0')
  })
})

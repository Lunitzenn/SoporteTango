import './commands'

Cypress.on('uncaught:exception', (err, runnable) => {
  // Evitar fallos por excepciones inesperadas del frontend de terceros (Bootstrap/jQuery)
  return false
})

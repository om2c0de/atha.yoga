/// <reference types = "cypress" />
import { slowCypressDown } from 'cypress-slow-down';
import { athaUsers } from '../../data/atha-users';

slowCypressDown(100);

describe('Восстановление пароля', () => {
  it('Восстановление пароля', () => {
    cy.visit('/');
    cy.get(':nth-child(2) > .MuiTypography-root').click();
    cy.get('[style="text-align: right;"] > .MuiTypography-root').click();
    cy.wait(2000);
    cy.get('#email').click().type(athaUsers.users.email);
    cy.get('.MuiButtonBase-root').click();
  });
});

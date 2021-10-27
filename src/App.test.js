/* eslint-disable*/
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('1. artist added to list', () => {
  render(<App />);
  const addButton = screen.getByText("Add artist");
  expect(addButton).toBeInTheDocument();
  const inputEl = screen.getByTestId("input-artist");
  fireEvent.change(inputEl, { target: { value: "test" } });
  fireEvent.click(addButton);

  const newItem = screen.getByText("test");
  expect(newItem).toBeInTheDocument();
});

test('2. artist removed from list', () => {
  render(<App />);
  const removeButton = screen.getByText("Remove");
  expect(removeButton).toBeInTheDocument();
  const todelete = screen.getByText("todelete");
  fireEvent.click(removeButton);

  expect(todelete).not.toBeInTheDocument();
});

test('3. list updated on save', () => {
  render(<App />);
  // delete artist
  const removeButton = screen.getByText("Remove");
  expect(removeButton).toBeInTheDocument();
  const todelete = screen.getByText("todelete");
  fireEvent.click(removeButton);
  // add artist
  const addButton = screen.getByText("Add artist");
  expect(addButton).toBeInTheDocument();
  const inputEl = screen.getByTestId("input-artist");
  fireEvent.change(inputEl, { target: { value: "78rUTD7y6Cy67W1RVzYs7t" } });
  fireEvent.click(addButton);
  const newItem = screen.getByText("78rUTD7y6Cy67W1RVzYs7t");
  // save
  const saveButton = screen.getByText("Save");
  expect(saveButton).toBeInTheDocument();
  fireEvent.click(saveButton);
  expect(newItem).toBeInTheDocument();
  expect(todelete).not.toBeInTheDocument();

});
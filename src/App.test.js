/* eslint-disable*/
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('1. artist added to list', () => {
  render(<App />);
  const addButton = screen.getByText("Add artist");
  expect(addButton).toBeInTheDocument();
  const inputEl = screen.getByTestId("input-artist");
  fireEvent.change(inputEl, {target: {value: "test"}});
  fireEvent.click(addButton);

  const newItem = screen.getByText("test");
  expect(newItem).toBeInTheDocument();
});


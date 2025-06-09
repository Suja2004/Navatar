const API_URL = "https://navatar-ashen.vercel.app";

export async function getBookings() {
  const response = await fetch(`${API_URL}/bookings/`);
  if (!response.ok) throw new Error("Failed to fetch bookings");
  return response.json();
}

export async function createBooking(booking) {
  const response = await fetch(`${API_URL}/bookings/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(booking),
  });
  if (!response.ok) throw new Error("Failed to create booking");
  return response.json();
}

export async function deleteBooking(id) {
  const response = await fetch(`${API_URL}/bookings/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) throw new Error("Failed to delete booking");
  return response.ok;
}

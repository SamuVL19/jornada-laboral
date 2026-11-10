const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

async function handleResponse(response) {
  if (!response.ok) {
    let errorData = null;
    try {
      errorData = await response.json();
    } catch {
      // Si la respuesta no es un JSON válido
    }

    if (errorData?.detail?.message) {
      const error = new Error(errorData.detail.message);
      error.code = errorData.detail.code;
      throw error;
    }

    throw new Error(response.statusText || 'Error en la solicitud');
  }

  return response.json();
}

export const shiftsApi = {
  async startShift(identificationCode) {
    const response = await fetch(`${BASE_URL}/shifts/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ identification_code: identificationCode }),
    });
    return handleResponse(response);
  },

  async endShift(identificationCode) {
    const response = await fetch(`${BASE_URL}/shifts/end`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ identification_code: identificationCode }),
    });
    return handleResponse(response);
  },

async getCurrentStatus(identificationCode) {
    const response = await fetch(`${BASE_URL}/shifts/current/${identificationCode}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    return handleResponse(response);
  },
};

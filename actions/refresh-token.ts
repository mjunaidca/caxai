export const refreshToken = async (refresh_token: string) => {
    const formData = new FormData();
    formData.append('refresh_token', refresh_token);
    formData.append('grant_type', 'refresh_token');
  
    const response = await fetch(`${process.env.BACKEND_URL}/api/token`, {
      method: 'POST',
      body: formData,
    });
  
    if (!response || response.status !== 200) {
      throw new Error('Token refresh failed');
    }
  
    const responseData = await response.json();
  
    return responseData;
  };
  
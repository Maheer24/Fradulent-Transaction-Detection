import axios from "axios";
import { saveAs } from "file-saver";

export const downloadFile = async (filename) => {
  try {
    const response = await axios.get(`http://localhost:8000/download_csv/?filename=${filename}`, {
      responseType: "blob",
    });
    saveAs(response.data, `${filename}_predicted.csv`);
  } catch (error) {
    alert("Error downloading file");
  }
};

export const generateImage = async (filename) => {
  try {
    const response = await axios.post(
      `http://localhost:8000/display_images/?filename=${filename}`,
      { filename }
    );
    return response.data;  // Return the data containing URLs for all charts
  } catch (error) {
    alert("Error generating images:", error);
  }
};


// export const generateImage = async (filename) => {
//   try {
//     // const response = await axios.post(`http://localhost:8000/display_images/?filename=${filename}`);
//     const response = await axios.post(`http://localhost:8000/display_images/?filename=${filename}`, {
//       filename,
//     });
//     return response.data.image_url;
//   } catch (error) {
//     alert("Error generating image:", error);
//   }
// }


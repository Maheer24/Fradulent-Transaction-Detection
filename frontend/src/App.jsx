import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import DataTable from "./components/DataTable";
import { downloadFile, generateImage } from "./services/api";

const App = () => {
  const [data, setData] = useState([]);
  const [filename, setFilename] = useState("");
  const [imageUrls, setImageUrls] = useState([]);  // Updated to store multiple images
  const [loadingImage, setLoadingImage] = useState(false);

  const handleGenerateImage = async () => {
    setLoadingImage(true);
    try {
      const response = await generateImage(filename);
      if (response) {
        // Set the array of image URLs
        setImageUrls([
          response.pie_image_url,
          response.ip_box_plot_url,
        ]);
      }
    } catch (error) {
      console.error("Error generating images:", error);
    }
    setLoadingImage(false);
  };

  return (
    <div className="container">
      <h2>Fraud Detection</h2>

      <FileUpload setData={setData} setFilename={setFilename} />

      {filename && (
        <>
          <button onClick={() => downloadFile(filename)}>Download</button>
          <button onClick={handleGenerateImage} disabled={loadingImage}>
            {loadingImage ? "Generating..." : "Generate Insights"}
          </button>
        </>
      )}
      
      <DataTable data={data} />

      {imageUrls.length > 0 && (
        <div>
          <h3>Insights</h3>
          {/* Render each image dynamically */}
          {imageUrls.map((url, index) => (
            <div key={index}>
              <h4>Chart {index + 1}</h4>
              <img
                src={`http://localhost:8000${url}`}
                alt={`chart-${index}`}
                style={{ maxWidth: "100%" }}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default App;


// const App = () => {
//   const [data, setData] = useState([]);
//   const [filename, setFilename] = useState("");
//   const [imageUrl, setImageUrl] = useState("");
//   const [loadingImage, setLoadingImage] = useState(false);

//   const handleGenerateImage = async () => {
//     setLoadingImage(true);
//     const url = await generateImage(filename);
//     if (url) {
//       setImageUrl(`http://localhost:8000${url}`);
//     }
//     setLoadingImage(false);
//   };

//   return (
//     <div className="container">

//       <h2>Fraud Detection</h2>

//       <FileUpload setData={setData} setFilename={setFilename} />
      
//       {filename && (
//         <>
//           <button onClick={() => downloadFile(filename)}>Download</button>
//           <button onClick={handleGenerateImage} disabled={loadingImage}>
//             {loadingImage ? "Generating..." : "Generate Insights"}
//           </button>
//         </>
//       )}
//       {/*{<button onClick={() => downloadFile(filename)}>Download</button>}*/}
//       <DataTable data={data} />
//       {imageUrl && (
//         <div>
//           <h3>Insights</h3>
//           <img src={imageUrl} alt="status plot" style={{ maxWidth: "100%"}} />
//         </div>
//       )}
//     </div>
//   );
// };

// export default App;

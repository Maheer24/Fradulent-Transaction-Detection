import React from "react";
import "../styles.css";

const DataTable = ({ data }) => {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {data.length > 0 && Object.keys(data[0]).map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index} className={
              row.status === "Normal" ? "normal" :
              row.status === "Anomalous" ? "anomalous" : "fraudulent"
            }>
              {Object.values(row).map((value, idx) => (
                <td key={idx}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
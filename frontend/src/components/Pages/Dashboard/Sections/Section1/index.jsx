import { useDispatch, useSelector } from "react-redux";
import { setSection1DataReducer } from "../../../../../Store/Slices/Section1/section1Slice";
import { useEffect, useState } from "react";
import { CardComponent } from "../../../../common/CardComponent";
import { fetchMetrics } from "../../../../../hook/fetchMetrics";
import { section1Selector } from "../../../../../Store/Slices/Section1/section1Selector";
import PieChartComponent from "../../../../Charts/PieChart";
import TableComponent from "../../../../common/TableComponent";
import StackedBarChartCard from "../../../../Charts/StackedBarChart";

function Section1() {
  const dispatch = useDispatch();
  const section1Data = useSelector(section1Selector);
  
  // 1. Add a local loading flag to prevent rendering a blank canvas
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    const url = "http://127.0.0.1:8000/api/dashboard/section1";
    
    fetchMetrics(url)
      .then((sectiondata) => {
        // Dispatch data straight to your Redux state layer
        dispatch(setSection1DataReducer(sectiondata));
        // Turn off loading once the Redux store has been updated
        setIsLoading(false);
      })
      .catch((err) => {
        console.error("Failed fetching data from endpoint:", err);
        setIsLoading(false);
      });
  }, [dispatch]); // Safe rule boundary inclusion

  // 2. The Protective Firewall: Wait until loading is false and the array keys exist
  if (isLoading || !section1Data || !section1Data.representation_ratio) {
    return (
      <div className="flex items-center justify-center h-64 w-full p-6 text-slate-400 animate-pulse font-medium text-sm">
        Calculating backend data matrices...
      </div>
    );
  }

  // 3. Render safe knowing your array payload is fully populated
  return (
    <div className="space-y-6 p-6 animate-fadeIn w-full">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <div className="md:col-span-1">
          <PieChartComponent 
            title="Overall Representation Ratio" 
            data={section1Data.representation_ratio}
            dataKey="count"  // Extracted dynamically by Recharts
            nameKey="gender" // Maps labels directly to your legends
          />
          <TableComponent 
            headers={["Employment Status Tier", "Male", "Female", "Total Segment"]}
            rows={section1Data.employment_matrix}
            keys={["status", "male", "female", "total"]}
          />
          <StackedBarChartCard
            title="Highest Education Attainment Level By Gender"
            data={section1Data.education_gender_matrix}
            xKey="education"
          /> 
        </div>

      </div>
    </div>
  );
}

export default Section1;
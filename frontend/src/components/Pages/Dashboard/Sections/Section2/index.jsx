import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { CardComponent } from "../../../../common/CardComponent";
import { fetchMetrics } from "../../../../../hook/fetchMetrics";
import { setSection2DataReducer } from "../../../../../Store/Slices/Section2/section2Slice";
import VerticalBarChartCard from "../../../../Charts/VerticalBarChart";
import { section2Selector } from "../../../../../Store/Slices/Section2/section2Selector";
import Heatmap from "../../../../Charts/Heatmap";

function Section2() {
  const dispatch = useDispatch();
  const section2Data = useSelector(section2Selector);
  

useEffect(() => {
    const url = "http://127.0.0.1:8000/api/dashboard/section2"
    const sectiondata = fetchMetrics(url)
    .then((sectiondata)=>{
      console.log(sectiondata);
      dispatch(setSection2DataReducer(sectiondata));
    })
  }, []); // Empty array ensures this only runs ONCE when the component mounts




  return (
    <div className="grid grid-cols-1 gap-6 w-full">
      <div className="col-span-1">
        <VerticalBarChartCard
          title="Academic Attainment Ladder"
          data={section2Data.attainment_ladder}
          xKey="level"
          yKey="count"
        />
      </div>
      <div>
        <Heatmap
          title="Highest Education vs. Employment Status Hotspots"
          xLabels={section2Data?.education_employment_matrix?.x_labels} 
          yLabels={section2Data?.education_employment_matrix?.y_labels} 
          data={section2Data?.education_employment_matrix?.matrix_data}
          dataKey="level"
        />
        
      </div>
    </div>
  )
}

export default Section2
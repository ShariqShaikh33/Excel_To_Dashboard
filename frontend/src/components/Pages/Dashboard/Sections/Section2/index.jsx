import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { CardComponent } from "../../../../common/CardComponent";
import { fetchMetrics } from "../../../../../hook/fetchMetrics";
import { setSection2DataReducer } from "../../../../../Store/Slices/Section2/section2Slice";

function Section2() {
  const dispatch = useDispatch();
  

useEffect(() => {
    const url = "http://127.0.0.1:8000/api/dashboard/section2"
    const sectiondata = fetchMetrics(url)
    .then((sectiondata)=>{
      console.log(sectiondata);
      dispatch(setSection2DataReducer(sectiondata));
    })
  }, []); // Empty array ensures this only runs ONCE when the component mounts




  return (
    <div>Section2</div>
  )
}

export default Section2
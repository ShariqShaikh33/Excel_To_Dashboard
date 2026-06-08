import { createSlice } from "@reduxjs/toolkit";

export const section2Slice = createSlice({
    name:"Section2",
    initialState: {},
    reducers:{
        setSection2DataReducer:(state,action)=>{
            return{...state,...action.payload};
        }
    }
})

export const {setSection2DataReducer} = section2Slice.actions;
export default section2Slice.reducer;
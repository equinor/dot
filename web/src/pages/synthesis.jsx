import React from "react";

import { useProjectContext } from "../components/context";
//import DBGraphFrame from '../features/visualization/db/DBGraphFrame';

function Synthesis() {
  const [project, setProjectContext] = useProjectContext();

  /* const fetchData = async () => {
    const updatedData = await readIssues(project);
    console.log("updatedData:");
    console.log(updatedData);

    setIssueList(updatedData);
    setProj(project);
    console.log("issueList:");
    console.log(updatedData);
  }
  useEffect(() => {
    fetchData()
  }, []) */

  return (
    <>Hello</>
    /*  <ProjectContext.Provider value={proj}>
      <><AppHeader />
        <FramingTabs />
      </>
    </> */
  );
}

export default Synthesis;

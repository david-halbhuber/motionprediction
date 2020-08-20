using System.Collections;
using System.Collections.Generic;
using UnityEngine;


// Das ist eine potentielle Lösung, um die Kamera in jedem Frame auf die Position des GameObjects, das sich zwischen den Augen befindet, zu setzen. Ich vermute, dass ihr das Problem mit der Kamera hattet,
// weil euch SteamVR die Position der Kamera kontinuierlich überschrieben hat. --> Kamera befindet sich außerhalb der Szene. Da wird das InputTracking von Steam disablen und die Kamera manuell auf die Augenposition setzen,
// wird lediglich die Rotation über das HMD geregelt.
public class SetCameraPosition : MonoBehaviour
{
    // GameObject can be referenced in the Inspector (Create and place a GameObject in the center of the eyes)
    public GameObject centerBetweenEyes;

    // Start is called before the first frame update
    void Start()
    {
        UnityEngine.XR.InputTracking.disablePositionalTracking = true;
        transform.position = centerBetweenEyes.transform.position;
        transform.rotation = centerBetweenEyes.transform.rotation;
    }

    // Update is called once per frame
    void Update()
    {
        // Set Camera Position to Position of GameObject between eyes
        transform.position = centerBetweenEyes.transform.position;
        transform.rotation = centerBetweenEyes.transform.rotation;

    }
}

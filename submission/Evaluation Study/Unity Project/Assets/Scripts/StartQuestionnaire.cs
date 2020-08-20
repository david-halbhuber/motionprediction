using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class StartQuestionnaire : MonoBehaviour
{

    public QuestionnaireControl questionnaireControl;
    
    void Start()
    {
        GetComponent<TextMeshPro>().faceColor = new Color32(23, 207, 214, 255);
        gameObject.SetActive(false);
    }

    void OnTriggerEnter(Collider other)
    {
        questionnaireControl.StartQuestionnaire();
        gameObject.SetActive(false);
    }
}

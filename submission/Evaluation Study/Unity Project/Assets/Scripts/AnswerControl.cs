using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class AnswerControl : MonoBehaviour
{
    // public properties
    public int optionId;
    public Renderer backgroundCube;
    public GameObject forwardButton;

    // private properties
    private Toggle toggle;
    private TextMeshPro optionText;
    private static Color32 activeColor = new Color32(255, 186, 8, 255);
    private static Color32 activeBgColor = new Color32(0, 166, 166, 255);
    private static Color32 inactiveColor = new Color32(255, 186, 8, 255);
    private static Color32 inactiveBgColor = new Color32(36, 36, 30, 255);

    void Awake()
    {
        toggle = GetComponent<Toggle>();
        optionText = GetComponent<TextMeshPro>();

        // render inactive colors 
        backgroundCube.material.color = inactiveBgColor;
        optionText.faceColor = inactiveColor;
    }

    void OnTriggerEnter(Collider other)
    {
        forwardButton.SetActive(true);
        toggle.isOn = !toggle.isOn;
    }

    public void OnChangeValue()
    {
        backgroundCube.material.color = toggle.isOn ? activeBgColor : inactiveBgColor;
        optionText.faceColor = toggle.isOn ? activeColor : inactiveColor;
    }
}
